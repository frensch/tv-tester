## Install
virtualenv venv     
source venv/bin/activate
pip install -r requirements.txt

## Config
export TEST_MODE=prepare or validate or run

### prepare
Deve ser começar neste modo para aprender como o app estável se comporta

### validate
Deve ser usado em seguida com prepare para validar a taxa de erro de comparação de imagens identicas

### run
Esse modo vai ser usado para realmente validar a versão que precisa ser validada

## run tests
prepare.sh
validate.sh
run.sh