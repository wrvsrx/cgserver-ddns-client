{
  stdenv,
  python3,
}:
stdenv.mkDerivation {
  name = "cgserver-ddns-client";
  buildInputs = [
    (python3.withPackages (
      ps: with ps; [
        distro
        psutil
        pynvml
        pydantic
      ]
    ))
  ];
  src = ./.;
  installPhase = ''
    mkdir -p $out/bin
    cp clienttask.py $out/bin/
    install -m755 main.py $out/bin/$name
    runHook postInstall
  '';
}
