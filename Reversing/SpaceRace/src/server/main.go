package main

import (
	"bufio"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"math"
	"math/rand"
	"os"
	"sync"
	"time"
)

type Obstacle struct {
	S float64 // along-track position (world units)
	X float64 // lateral center position (wu)
	W float64 // width (wu)
}

type ObsView struct {
	DY float64 `json:"dy"` // distance ahead from rover (wu)
	X  float64 `json:"x"`  // lateral center (wu)
	W  float64 `json:"w"`  // width (wu)
}

type TrackInfo struct {
	Length    float64 `json:"length"`
	HalfWidth float64 `json:"half_width"`
	Unit      string  `json:"unit"`
}

type Telemetry struct {
	T           string     `json:"t"`
	Time        float64    `json:"time"`
	S           float64    `json:"s"`
	X           float64    `json:"x"`
	Vel         float64    `json:"vel"`
	HeadingDeg  float64    `json:"heading_deg"`
	ThrottlePct int        `json:"throttle_pct"`
	SteerPct    int        `json:"steer_pct"`
	Status      string     `json:"status"` // ok | crashed | finished
	Track       TrackInfo  `json:"track"`
	Obstacles   []ObsView  `json:"obstacles"`
	Msg         string     `json:"msg"`
	Flag        *string    `json:"flag"`
}

type ControlMsg struct {
	T     string `json:"t"`
	Frame string `json:"frame"`
}

const (
	telemetryHz   = 12
	physicsHz     = 60
	trackLen      = 1000.0 // world units
	trackHalf     = 60.0   // half width (wu)
	roverWidth    = 10.0   // wu
	turnFactor    = 0.5    // dx/dt = (steerPct/100)*turnFactor*vel
	accelPerPct   = 0.11   // wu/s^2 per throttle pct
	drag          = 0.996  // velocity damping per tick
	brakeFactor   = 0.65   // one-shot damp
	visibleAhead  = 180.0  // wu in front to include in telemetry
	collisionDY   = 3.0    // collide when crossing within this dy window
	finishSlackX  = trackHalf - roverWidth/2 - 1
)

type Rover struct {
	mu          sync.Mutex
	s           float64 // along-track distance
	x           float64 // lateral offset (-trackHalf..+trackHalf)
	vel         float64 // forward speed (wu/s)
	heading     float64 // cosmetic, radians
	throttlePct int     // 0..100
	steerPct    int     // -100..100
	status      string  // ok | crashed | finished
	msg         string
	flagSent    bool
}

func clampInt(v, lo, hi int) int {
	if v < lo {
		return lo
	}
	if v > hi {
		return hi
	}
	return v
}

func clamp(v, lo, hi float64) float64 {
	if v < lo {
		return lo
	}
	if v > hi {
		return hi
	}
	return v
}

func makeCourse(seed int64) []Obstacle {
	r := rand.New(rand.NewSource(seed))
	var obs []Obstacle
	s := 140.0
	for s < trackLen-40 {
		if r.Float64() < 0.38 {
			w := 16.0 + r.Float64()*16.0
			x := (r.Float64()*2 - 1) * (trackHalf - w/2 - 5)
			obs = append(obs, Obstacle{S: s, X: x, W: w})
		}
		s += 38.0 + r.Float64()*55.0
	}
	return obs
}

func main() {
	seed := time.Now().Unix() & 0x7fffffff
	course := makeCourse(int64(seed))

	rover := &Rover{
		status: "ok",
		msg:    "Rover link up. Implement controls to move!",
	}

	// Physics loop
	go func() {
		tick := time.NewTicker(time.Second / physicsHz)
		defer tick.Stop()
		nextIdx := 0
		for range tick.C {
			rover.mu.Lock()
			if rover.status == "ok" {
				// heading (cosmetic)
				rover.heading += (float64(rover.steerPct) / 100.0) * (math.Pi / 180.0) * 0.8

				// forward accel/drag
				a := float64(rover.throttlePct) * accelPerPct
				rover.vel += a / float64(physicsHz)
				rover.vel *= drag

				// integrate forward and lateral
				rover.s += rover.vel / float64(physicsHz)
				rover.x += (float64(rover.steerPct) / 100.0) * turnFactor * rover.vel / float64(physicsHz)
				rover.x = clamp(rover.x, -trackHalf+roverWidth/2, trackHalf-roverWidth/2)

				// finish
				if rover.s >= trackLen {
					rover.status = "finished"
					rover.msg = "Finish reached! Transmitting flag…"
				}

				// collision check against upcoming obstacle
				for nextIdx < len(course) && course[nextIdx].S < rover.s-visibleAhead {
					nextIdx++
				}
				// Check any obstacle whose S is within small window around rover.s
				for i := nextIdx; i < len(course); i++ {
					if course[i].S < rover.s-collisionDY {
						continue
					}
					if course[i].S > rover.s+collisionDY {
						break
					}
					halfSum := roverWidth/2 + course[i].W/2
					if math.Abs(rover.x-course[i].X) <= halfSum {
						rover.status = "crashed"
						rover.vel *= 0.2
						rover.msg = "Crash! Press reset (0x205) to try again."
						break
					}
				}
			}
			rover.mu.Unlock()
		}
	}()

	// Telemetry loop
	go func() {
		w := bufio.NewWriter(os.Stdout)
		tick := time.NewTicker(time.Second / telemetryHz)
		defer tick.Stop()
		sentFlag := false
		for range tick.C {
			rover.mu.Lock()
			s := rover.s
			x := rover.x
			vel := rover.vel
			hdg := rover.heading * 180 / math.Pi
			th := rover.throttlePct
			st := rover.steerPct
			status := rover.status
			msg := rover.msg

			// window of obstacles ahead
			var view []ObsView
			for _, ob := range course {
				dy := ob.S - s
				if dy >= 0 && dy <= visibleAhead {
					view = append(view, ObsView{DY: dy, X: ob.X, W: ob.W})
				}
				if ob.S > s+visibleAhead {
					break
				}
			}

			var flag *string
			if status == "finished" && !sentFlag {
				f := "sun{r3d_r0v3r_c0m3_0v3r}"
				flag = &f
				sentFlag = true
			}
			rover.mu.Unlock()

			tel := Telemetry{
				T:           "telemetry",
				Time:        float64(time.Now().UnixNano()) / 1e9,
				S:           s,
				X:           x,
				Vel:         vel,
				HeadingDeg:  hdg,
				ThrottlePct: th,
				SteerPct:    st,
				Status:      status,
				Track:       TrackInfo{Length: trackLen, HalfWidth: trackHalf, Unit: "wu"},
				Obstacles:   view,
				Msg:         msg,
				Flag:        flag,
			}
			b, _ := json.Marshal(tel)
			fmt.Fprintln(w, string(b))
			_ = w.Flush()
		}
	}()

	// Controls loop (stdin)
	reader := bufio.NewReader(os.Stdin)
	for {
		line, err := reader.ReadBytes('\n')
		if err != nil {
			if err == io.EOF {
				time.Sleep(30 * time.Millisecond)
				continue
			}
			return
		}
		var msg ControlMsg
		if err := json.Unmarshal(trim(line), &msg); err != nil {
			continue
		}
		if msg.T != "can" || msg.Frame == "" {
			continue
		}
		raw, err := hex.DecodeString(msg.Frame)
		if err != nil || len(raw) < 3 {
			continue
		}
		id := (uint16(raw[0]) << 8) | uint16(raw[1])
		dlc := int(raw[2] & 0x0F)
		if dlc < 0 || dlc > 8 || len(raw) < 3+dlc {
			continue
		}
		data := raw[3 : 3+dlc]

		rover.mu.Lock()
		switch id & 0x7FF {
		case 0x201: // throttle
			if dlc >= 1 {
				rover.throttlePct = clampInt(int(data[0]), 0, 100)
				rover.msg = fmt.Sprintf("Throttle %d%%", rover.throttlePct)
			}
		case 0x202: // steering
			if dlc >= 1 {
				sp := int(int8(data[0]))
				rover.steerPct = clampInt(sp, -100, 100)
				rover.msg = fmt.Sprintf("Steer %d%%", rover.steerPct)
			}
		case 0x203: // brake
			rover.vel *= brakeFactor
			rover.msg = "Brake!"
		case 0x204: // stabilize
			rover.steerPct = 0
			rover.heading *= 0.9
			rover.msg = "Stabilizers on"
		case 0x205: // reset
			if rover.status != "ok" {
				rover.s, rover.x, rover.vel = 0, 0, 0
				rover.throttlePct, rover.steerPct = 0, 0
				rover.status = "ok"
				rover.msg = "Reset to start"
			}
		default:
			rover.msg = fmt.Sprintf("Unknown CAN 0x%03X", id&0x7FF)
		}
		rover.mu.Unlock()
	}
}

func trim(b []byte) []byte {
	i, j := 0, len(b)
	for i < j && (b[i] == ' ' || b[i] == '\t' || b[i] == '\r' || b[i] == '\n') {
		i++
	}
	for i < j && (b[j-1] == ' ' || b[j-1] == '\t' || b[j-1] == '\r' || b[j-1] == '\n') {
		j--
	}
	return b[i:j]
}
