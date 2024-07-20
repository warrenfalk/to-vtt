{
  description = "A Nix flake for the Whisper ASR model";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";  # You can pin this to a specific version if you like
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        system = "x86_64-linux";
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
          config.cudaSupport = true;
        };

      in
      {
        devShell = pkgs.mkShell {
          buildInputs = [
            pkgs.python3  # Latest Python
            #pkgs.python3Packages.pytorchWithCuda  # PyTorch package
            #pkgs.python3Packages.pytorch  # PyTorch package
            #pkgs.python3Packages.transformers
            #pkgs.python3Packages.datasets
            #pkgs.python3Packages.soundfile
            #pkgs.python3Packages.librosa
            #pkgs.python3Packages.pyaudio
            #pkgs.python3Packages.scipy
            #pkgs.python3Packages.matplotlib
            #pkgs.python3Packages.tiktoken
            #pkgs.python3Packages.google-api-python-client
            #pkgs.python3Packages.google-auth-httplib2
            #pkgs.python3Packages.google-auth-oauthlib
            #pkgs.python3Packages.speechrecognition
            #audiostretchy
            #pyrubberband
            # for the server
            #pkgs.python3Packages.websockets
            # just for testing
            #pkgs.sox
            #pkgs.pulseaudio
            # this requires allowUnfree in the config
            #pkgs.cudatoolkit
            #pkgs.linuxPackages.nvidia_x11
            #pkgs.cudaPackages.cudnn
            #pkgs.libGLU
            #pkgs.libGL
            #pkgs.xorg.libXi
            #pkgs.xorg.libXmu
            #pkgs.freeglut
            #pkgs.xorg.libXext
            #pkgs.xorg.libX11
            #pkgs.xorg.libXv
            #pkgs.xorg.libXrandr
            #pkgs.zlib 
            #pkgs.ncurses5
            #pkgs.stdenv.cc
            #pkgs.binutils
            #pkgs.ffmpeg
          ];
          # Environment variables can be set here if needed

          shellHook = ''
            export PS1="(devenv) $PS1"
            export HISTFILE=.bash_history
            export LD_LIBRARY_PATH=${pkgs.linuxPackages.nvidia_x11}/lib:${pkgs.cudatoolkit}/lib64:$LD_LIBRARY_PATH
          '';
        };
      }
    );
}
