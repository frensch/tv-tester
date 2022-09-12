## Install
virtualenv venv     
source venv/bin/activate
pip install -r requirements.txt

## Config
export TEST_MODE=capture or validate or run

### capture
Deve ser começar neste modo para aprender como o app estável se comporta

### validate
Deve ser usado em seguida com capture para validar a taxa de erro de comparação de imagens identicas

### run
Esse modo vai ser usado para realmente validar a versão que precisa ser validada

## run tests
capture.sh
validate.sh
run.sh