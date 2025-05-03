{
  buildPythonPackage,
  hatchling,

  distro,
  psutil,
  pynvml,
  pydantic,
}:
buildPythonPackage {
  pname = "cgserver-ddns-client";
  version = "0-unstable-dev";
  pyproject = true;
  src = ./.;
  nativeBuildInputs = [
    hatchling
  ];
  dependencies = [
    distro
    psutil
    pynvml
    pydantic
  ];
}
