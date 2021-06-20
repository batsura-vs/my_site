sonar-scanner \
  -Dsonar.projectKey=vova \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  "-Dsonar.exclusions=venv/**, static/**" \
  -Dsonar.login=2682cf20f3d85b07de0276d14c0598959b884dcc
