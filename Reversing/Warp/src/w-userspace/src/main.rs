use aya::maps::RingBuf;
use aya::programs::{Xdp, XdpFlags};
use aya::Ebpf;
use std::env;
use std::ffi::CStr;
use std::mem;
use std::fs::File;
use std::io::{BufReader, BufRead};

#[repr(C)]
#[derive(Copy, Clone)]
struct Event {
    pub text: [u8; 32],
    pub is_flag: u8,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Bump the memlock rlimit. This is needed for older kernels that don't use the
    // new memcg based accounting, see https://lwn.net/Articles/837122/
    let rlim = libc::rlimit {
        rlim_cur: libc::RLIM_INFINITY,
        rlim_max: libc::RLIM_INFINITY,
    };
    let _ = unsafe { libc::setrlimit(libc::RLIMIT_MEMLOCK, &rlim) };

    let mut ebpf = Ebpf::load(aya::include_bytes_aligned!(concat!(
            env!("OUT_DIR"),
            "/main.bpf.o"
        )))?;
    
    let iface = default_iface_linux()?
        .ok_or_else(|| "No default interface found")?;

    let prog: &mut Xdp = ebpf.program_mut("xdp_prog").unwrap().try_into()?;
    prog.load()?;
    // SKB_MODE instead of default() since virtual adapters don't support hardware xdp
    prog.attach(&iface, XdpFlags::SKB_MODE)?;

    let mut rb = RingBuf::try_from(ebpf.map_mut("rb").unwrap())?;

    println!("This proram is listening...");
    
    loop {
        // avoiding tokio channels to make ppl doing static rev the rust hate me a bit less
        std::thread::sleep(std::time::Duration::from_millis(5));
        if let Some(item) = rb.next() {
            let buffer: [u8; mem::size_of::<Event>()] = (*item).try_into()?;
            let event: Event = unsafe { mem::transmute(buffer) };
            let str = get_str(&event.text);
            if event.is_flag == 0 {
                println!("Message recieved, no flag warped. {}", str);
            } else {
                println!("Oh look! A flag came out of the warp tunnel! {}", str);
            }
        }
    }
}

/// Converts a (potentially) null-terminated u8 character array into a `String`
fn get_str(bytes: &[u8]) -> String {
    if let Some(len) = bytes.iter().position(|&c| c == 0) {
        let nul_terminated = &bytes[..=len];
        if let Ok(cstr) = CStr::from_bytes_with_nul(nul_terminated) {
            if let Ok(valid_str) = cstr.to_str() {
                return valid_str.to_owned();
            }
        }
    }

    String::from_utf8_lossy(bytes).into_owned()
}

fn default_iface_linux() -> std::io::Result<Option<String>> {
    let f = File::open("/proc/net/route")?;
    let reader = BufReader::new(f);

    // /proc/net/route columns:
    // Iface  Destination  Gateway  Flags  RefCnt  Use  Metric  Mask  MTU  Window  IRTT
    // Default route has Destination == "00000000" (hex)
    for (i, line) in reader.lines().enumerate() {
        let line = line?;
        if i == 0 { continue; }
        let cols: Vec<&str> = line.split('\t').collect();
        if cols.len() >= 11 {
            let iface = cols[0];
            let destination = cols[1];
            let flags_hex = u16::from_str_radix(cols[3], 16).unwrap_or(0);
            let rtf_up = 0x0001;      // RTF_UP
            let rtf_gateway = 0x0002; // RTF_GATEWAY

            if destination == "00000000" && (flags_hex & rtf_up) != 0 && (flags_hex & rtf_gateway) != 0 {
                return Ok(Some(iface.to_string()));
            }
        }
    }
    Ok(None)
}
