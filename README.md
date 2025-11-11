# Tintim-Clima (Django + DRF)

## 1) Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## 2) Banco e admin
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
- Admin: http://127.0.0.1:8000/admin/
- Ajuste limite/intervalo/lat/lon em **Settings** (será criado automaticamente na 1ª execução do job)

## 3) Endpoints (DRF)
- `GET /api/latest/` → última leitura
- `GET /api/trigger-fetch/` → força coleta e regra (header `X-API-KEY` com `API_TEST_TOKEN`)

Exemplos:
```bash
curl http://127.0.0.1:8000/api/latest/
curl -H "X-API-KEY: meu-token-de-teste" http://127.0.0.1:8000/api/trigger-fetch/
```

## 4) Cron (agendamento)
```bash
python manage.py crontab add
python manage.py crontab show
# remover
python manage.py crontab remove
```
- O cron agenda a cada 5 min, e o job respeita `CHECK_EVERY_MIN`.

## 5) Testes
```bash
python manage.py test
```

## 6) Deploy simples
- Configure variáveis do `.env` na plataforma (Render/Railway/PythonAnywhere etc.)
- Use `Procfile` (Gunicorn)
- Para agendamentos, use `django-crontab` **ou** o scheduler nativo da plataforma para rodar periodicamente um comando que invoque `weather.cron.run_check()`
# tintim-desafio
# tintim-desafio
