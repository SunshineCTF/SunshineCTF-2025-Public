{
  description = "Warp ebpf: A Crane-based Nix build";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    rust-overlay.url = "github:oxalica/rust-overlay";
    crane = {
      url = "github:ipetkov/crane";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, rust-overlay, crane }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        overlays = [ (import rust-overlay) ];
        pkgs = import nixpkgs {
          inherit system overlays;
        };
        muslPkgs = pkgs.pkgsCross.musl64;

        # Rust toolchain with musl target
        rustToolchain = pkgs.rust-bin.stable.latest.default.override {
          targets = [ "x86_64-unknown-linux-musl" ];
        };

        # Crane library instance configured for our toolchain
        craneLib = crane.mkLib pkgs;

        # Create crane lib with our custom toolchain
        craneLibWithToolchain = craneLib.overrideToolchain rustToolchain;

        # Common build inputs
        commonBuildInputs = with pkgs; [
          clang
          llvm
          llvmPackages.llvm
          pkg-config
          cmake
          git
          gnumake
          # eBPF development tools
          bpftools
          linuxPackages.bcc
          linuxPackages.bpftrace
        ];

        # Musl-specific build inputs
        muslBuildInputs = commonBuildInputs ++ (with muslPkgs; [
          stdenv.cc
          elfutils
          elfutils.dev
          libbpf
          zlib.dev
          openssl.dev
        ]);

        # Use path directly to include all files
        src = craneLib.path ./.;

        # Common environment variables for musl builds
        muslEnvVars = {
          CARGO_BUILD_TARGET = "x86_64-unknown-linux-musl";
          CARGO_TARGET_X86_64_UNKNOWN_LINUX_MUSL_LINKER = "${muslPkgs.stdenv.cc}/bin/x86_64-unknown-linux-musl-gcc";
          CC_x86_64_unknown_linux_musl = "${muslPkgs.stdenv.cc}/bin/x86_64-unknown-linux-musl-gcc";
          CXX_x86_64_unknown_linux_musl = "${muslPkgs.stdenv.cc}/bin/x86_64-unknown-linux-musl-g++";
          AR_x86_64_unknown_linux_musl = "${muslPkgs.stdenv.cc}/bin/x86_64-unknown-linux-musl-ar";
          CARGO_TARGET_X86_64_UNKNOWN_LINUX_MUSL_RUSTFLAGS = "-C target-feature=+crt-static -C link-arg=-lm";
          PKG_CONFIG_PATH = "${muslPkgs.elfutils.dev}/lib/pkgconfig:${muslPkgs.zlib.dev}/lib/pkgconfig:${muslPkgs.libbpf}/lib/pkgconfig";
          CFLAGS = "-I${muslPkgs.elfutils.dev}/include -I${muslPkgs.zlib.dev}/include -I${muslPkgs.libbpf}/include";
          LDFLAGS = "-L${muslPkgs.elfutils}/lib -L${muslPkgs.zlib}/lib -L${muslPkgs.libbpf}/lib";
          C_INCLUDE_PATH = "${muslPkgs.elfutils.dev}/include:${muslPkgs.zlib.dev}/include:${muslPkgs.libbpf}/include";
          LIBRARY_PATH = "${muslPkgs.elfutils}/lib:${muslPkgs.zlib}/lib:${muslPkgs.libbpf}/lib";
          RUST_BACKTRACE = "1";
        };

        # Build just the dependencies of the workspace to get better caching
        cargoArtifacts = craneLibWithToolchain.buildDepsOnly ({
          inherit src;
          pname = "warp-deps";
          version = "0.1.0";
          nativeBuildInputs = muslBuildInputs;
          preBuild = ''
            echo "Setting up libbpf using nixpkgs version"
            echo "Current directory: $(pwd)"
            echo "Directory contents:"
            ls -la
            echo "Looking for w-ebpf:"
            find . -name "*ebpf*" -type d || true
            echo "Contents of w-ebpf directory:"
            ls -la w-ebpf/ || echo "e-ebpf directory not found"
            echo "Looking for Makefile:"
            find . -name "Makefile*" || echo "No Makefile found"

            # Create directory structure that Makefile expects
            mkdir -p w-ebpf/libbpf/src

            # Copy libbpf.a to where Makefile expects it
            cp ${muslPkgs.libbpf}/lib/libbpf.a w-ebpf/libbpf/src/

            # Set environment variable to indicate this is a dependency-only build
            export CRANE_BUILD_DEPS_ONLY=1

          '';
        } // muslEnvVars);

        # Build the actual workspace
        warp-ebpf = craneLibWithToolchain.buildPackage ({
          inherit cargoArtifacts src;
          pname = "warp";
          version = "0.1.0";
          nativeBuildInputs = muslBuildInputs;

          preBuild = ''
            echo "Setting up libbpf for production build"
            echo "Current directory: $(pwd)"
            echo "Directory contents:"
            ls -la
            echo "Looking for w-ebpf:"
            find . -name "*ebpf*" -type d || true
            echo "Contents of w-ebpf directory:"
            ls -la w-ebpf/ || echo "e-ebpf directory not found"
            echo "Looking for Makefile:"
            find . -name "Makefile*" || echo "No Makefile found"

            # Create directory structure that Makefile expects
            mkdir -p w-ebpf/libbpf/src

            # Copy libbpf.a to where Makefile expects it
            cp ${muslPkgs.libbpf}/lib/libbpf.a w-ebpf/libbpf/src/


          '';

          # Skip tests for now
          doCheck = false;

          meta = with pkgs.lib; {
            description = "Warp ebpf binary built with Crane, statically linked with musl";
            license = licenses.mit;
            maintainers = [ "yourname" ];
          };
        } // muslEnvVars);

        # Development environment variables
        devEnvVars = {
          PKG_CONFIG_PATH = "${pkgs.elfutils.dev}/lib/pkgconfig:${pkgs.zlib.dev}/lib/pkgconfig:${pkgs.libbpf}/lib/pkgconfig";
          CFLAGS = "-I${pkgs.elfutils.dev}/include -I${pkgs.zlib.dev}/include -I${pkgs.libbpf}/include";
          LDFLAGS = "-L${pkgs.elfutils}/lib -L${pkgs.zlib}/lib -L${pkgs.libbpf}/lib";
          C_INCLUDE_PATH = "${pkgs.elfutils.dev}/include:${pkgs.zlib.dev}/include:${pkgs.libbpf}/include";
          LIBRARY_PATH = "${pkgs.elfutils}/lib:${pkgs.zlib}/lib:${pkgs.libbpf}/lib";
          RUST_BACKTRACE = "1";
        };

        # Build just the dependencies for development
        cargoArtifactsDev = craneLibWithToolchain.buildDepsOnly ({
          inherit src;
          pname = "warp-dev-deps";
          version = "0.1.0";
          nativeBuildInputs = commonBuildInputs ++ (with pkgs; [
            elfutils
            elfutils.dev
            libbpf
            zlib.dev
            openssl.dev
          ]);
          preBuild = ''
            echo "Setting up libbpf for development build dependencies"
            echo "Current directory: $(pwd)"
            echo "Directory contents:"
            ls -la
            echo "Looking for w-ebpf:"
            find . -name "*ebpf*" -type d || true
            echo "Contents of w-ebpf directory:"
            ls -la w-ebpf/ || echo "e-ebpf directory not found"
            echo "Looking for Makefile:"
            find . -name "Makefile*" || echo "No Makefile found"

            mkdir -p w-ebpf/libbpf/src
            cp ${pkgs.libbpf}/lib/libbpf.a w-ebpf/libbpf/src/

            # Set environment variable to indicate this is a dependency-only build
            export CRANE_BUILD_DEPS_ONLY=1

          '';
        } // devEnvVars);

        # Build for development (native, dynamically linked)
        warp-ebpf-dev = craneLibWithToolchain.buildPackage ({
          inherit src;
          cargoArtifacts = cargoArtifactsDev;
          pname = "warp-dev";
          version = "0.1.0";
          nativeBuildInputs = commonBuildInputs ++ (with pkgs; [
            elfutils
            elfutils.dev
            libbpf
            zlib.dev
            openssl.dev
          ]);

          preBuild = ''
            echo "Setting up libbpf for development build"
            echo "Current directory: $(pwd)"
            echo "Directory contents:"
            ls -la
            echo "Looking for w-ebpf:"
            find . -name "*ebpf*" -type d || true
            echo "Contents of w-ebpf directory:"
            ls -la w-ebpf/ || echo "e-ebpf directory not found"
            echo "Looking for Makefile:"
            find . -name "Makefile*" || echo "No Makefile found"

            mkdir -p w-ebpf/libbpf/src
            cp ${pkgs.libbpf}/lib/libbpf.a w-ebpf/libbpf/src/


          '';

          doCheck = false;
        } // devEnvVars);

        # Just run cargo check for faster feedback
        warp-ebpf-clippy = craneLibWithToolchain.cargoClippy ({
          inherit cargoArtifacts src;
          pname = "warp-clippy";
          version = "0.1.0";
          nativeBuildInputs = muslBuildInputs;
          cargoClippyExtraArgs = "--all-targets -- --deny warnings";
          preBuild = ''
            echo "Setting up libbpf for clippy"
            echo "Current directory: $(pwd)"
            echo "Directory contents:"
            ls -la
            echo "Looking for w-ebpf:"
            find . -name "*ebpf*" -type d || true
            echo "Contents of w-ebpf directory:"
            ls -la w-ebpf/ || echo "e-ebpf directory not found"
            echo "Looking for Makefile:"
            find . -name "Makefile*" || echo "No Makefile found"

            mkdir -p w-ebpf/libbpf/src
            cp ${muslPkgs.libbpf}/lib/libbpf.a w-ebpf/libbpf/src/
          '';
        } // muslEnvVars);

        # Run tests
        warp-ebpf-test = craneLibWithToolchain.cargoTest ({
          inherit cargoArtifacts src;
          pname = "warp-test";
          version = "0.1.0";
          nativeBuildInputs = muslBuildInputs;
          preBuild = ''
            echo "Setting up libbpf for tests"
            echo "Current directory: $(pwd)"
            echo "Directory contents:"
            ls -la
            echo "Looking for w-ebpf:"
            find . -name "*ebpf*" -type d || true
            echo "Contents of w-ebpf directory:"
            ls -la w-ebpf/ || echo "e-ebpf directory not found"
            echo "Looking for Makefile:"
            find . -name "Makefile*" || echo "No Makefile found"

            mkdir -p w-ebpf/libbpf/src
            cp ${muslPkgs.libbpf}/lib/libbpf.a w-ebpf/libbpf/src/
          '';
        } // muslEnvVars);

        # Check formatting
        warp-ebpf-fmt = craneLibWithToolchain.cargoFmt {
          inherit src;
          pname = "warp-fmt";
          version = "0.1.0";
          preBuild = ''
          '';
        };

      in {
        packages = {
          inherit warp-ebpf warp-ebpf-dev;
          default = warp-ebpf;

          # Additional packages for CI/development
          clippy = warp-ebpf-clippy;
          test = warp-ebpf-test;
          fmt = warp-ebpf-fmt;
        };

        checks = {
          inherit warp-ebpf warp-ebpf-clippy warp-ebpf-test warp-ebpf-fmt;
        };

        devShells.default = pkgs.mkShell {
          buildInputs = commonBuildInputs ++ (with pkgs; [
            # Use rust toolchain with musl target pre-installed
            rustToolchain
            # Build dependencies for development (using regular pkgs for faster dev builds)
            elfutils
            elfutils.dev
            libbpf
            zlib.dev
            openssl.dev
            # Cross-compilation toolchain
            muslPkgs.stdenv.cc
            # Development tools
            cargo-watch
            cargo-edit
            rust-analyzer
            # Additional LLVM tools for completeness
            llvmPackages.bintools
            llvmPackages.llvm
          ]);

          shellHook = ''
            echo "Setting up development environment with Crane"

            # Verify musl target is available
            if rustc --print target-list | grep -q "x86_64-unknown-linux-musl"; then
              echo "✓ x86_64-unknown-linux-musl target is available"
            else
              echo "✗ x86_64-unknown-linux-musl target is not available"
              exit 1
            fi

            # Set up libbpf in the expected location if it doesn't exist
            if [ ! -d "w-ebpf/libbpf/src" ]; then
              echo "Setting up libbpf..."
              mkdir -p w-ebpf/libbpf/src
              cp ${pkgs.libbpf}/lib/libbpf.a w-ebpf/libbpf/src/
            fi

            # Set environment variables for development builds (regular linking)
            export PKG_CONFIG_PATH="${pkgs.elfutils.dev}/lib/pkgconfig:${pkgs.zlib.dev}/lib/pkgconfig:${pkgs.libbpf}/lib/pkgconfig:$PKG_CONFIG_PATH"
            export CFLAGS="-I${pkgs.elfutils.dev}/include -I${pkgs.zlib.dev}/include -I${pkgs.libbpf}/include"
            export LDFLAGS="-L${pkgs.elfutils}/lib -L${pkgs.zlib}/lib -L${pkgs.libbpf}/lib"
            export C_INCLUDE_PATH="${pkgs.elfutils.dev}/include:${pkgs.zlib.dev}/include:${pkgs.libbpf}/include"
            export LIBRARY_PATH="${pkgs.elfutils}/lib:${pkgs.zlib}/lib:${pkgs.libbpf}/lib"
            export RUST_BACKTRACE=1

            # Set environment variables for musl cross-compilation
            export CARGO_TARGET_X86_64_UNKNOWN_LINUX_MUSL_LINKER="${muslPkgs.stdenv.cc}/bin/x86_64-unknown-linux-musl-gcc"
            export CC_x86_64_unknown_linux_musl="${muslPkgs.stdenv.cc}/bin/x86_64-unknown-linux-musl-gcc"
            export CXX_x86_64_unknown_linux_musl="${muslPkgs.stdenv.cc}/bin/x86_64-unknown-linux-musl-g++"
            export AR_x86_64_unknown_linux_musl="${muslPkgs.stdenv.cc}/bin/x86_64-unknown-linux-musl-ar"
            export CARGO_TARGET_X86_64_UNKNOWN_LINUX_MUSL_RUSTFLAGS="-C target-feature=+crt-static -C link-arg=-lm"

            # Set musl-specific environment variables for cross-compilation
            export PKG_CONFIG_PATH_x86_64_unknown_linux_musl="${muslPkgs.elfutils.dev}/lib/pkgconfig:${muslPkgs.zlib.dev}/lib/pkgconfig:${muslPkgs.libbpf}/lib/pkgconfig"
            export CFLAGS_x86_64_unknown_linux_musl="-I${muslPkgs.elfutils.dev}/include -I${muslPkgs.zlib.dev}/include -I${muslPkgs.libbpf}/include"
            export LDFLAGS_x86_64_unknown_linux_musl="-L${muslPkgs.elfutils}/lib -L${muslPkgs.zlib}/lib -L${muslPkgs.libbpf}/lib"

            echo "Development environment ready!"
            echo ""
            echo "Available commands:"
            echo "  For development (dynamically linked): cargo build --release"
            echo "  For musl cross-compilation: cargo build --release --target x86_64-unknown-linux-musl"
            echo "  For production (statically linked): nix build"
            echo "  For development build via Nix: nix build .#warp-ebpf-dev"
            echo ""
            echo "Crane-specific commands:"
            echo "  Check code: nix build .#clippy"
            echo "  Run tests: nix build .#test"
            echo "  Check formatting: nix build .#fmt"
            echo ""
            echo "Output locations:"
            echo "  Development binary: target/release/warp"
            echo "  Musl binary: target/x86_64-unknown-linux-musl/release/warp"
            echo "  Production binary: result/bin/warp"
          '';
        };
      }
    );
}
