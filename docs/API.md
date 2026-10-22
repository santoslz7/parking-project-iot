# Contrato da API (rascunho v0)

Base URL (dev): `http://localhost:5000`. Todas as respostas são JSON.
Erros: `{ "error": "mensagem" }`. Códigos: 200, 201, 400, 401, 403, 404, 409.

## GET /api/parking-lots
Lista locais ativos (campos públicos).

200:
```json
[{ "id": "centro", "name": "Unidade Centro", "address": "...",
   "latitude": -12.54, "longitude": -38.23, "hourly_rate": 8.0,
   "opening_hours": "06:00-22:00" }]
```

## GET /api/parking-lots/{id}/availability?arrival=...&departure=...
Datas em ISO 8601 **com fuso** (ex.: `2026-10-24T14:00:00-03:00`).

200:
```json
{ "parking_lot_id": "centro", "arrival": "...", "departure": "...",
  "total_spaces": 10, "available_spaces": 9,
  "available_space_ids": ["centro-A01"] }
```
400: período inválido (saída <= chegada, sem fuso, no passado). 404: local inexistente.

## POST /api/iot/access-request  (PENDENTE)
Header `X-Device-Secret`.
Body: `{ "event_id": "...", "device_id": "...", "type": "ENTRY|EXIT", "reservation_code": "..." }`
Resposta: `{ "authorized": true|false, "reason": "..." }`
