# Testes

**cwd = raiz do repositório.**

```text
python -m pytest
```

## Conteúdo (`tests/unit/`)

| Ficheiro | Uso |
|----------|-----|
| `conftest_minimal_config.py` | `minimal_valid_config()` para testes de `validate_config` |
| `test_trading_types.py` | `opposite_direction` (CALL/PUT/NONE) |
| `test_config_validation.py` | Secções obrigatórias e `validate_config` |
| `test_decision_service.py` | Gates e score (`entry_score`, penalidades, `direction_marginal`, etc.) |
| `test_adaptive_execution_policy.py` | Rebalance e anti-flip adaptativos |
| `test_vote_aggregation.py` | Qualidade de janela, maioria, bucket temporal, pseudo-score |
| `test_engine_logging_candles.py` | Seleção de vela e janela de contrato nos logs |
| `test_risk_manager.py` | sizing de risco, stake por saldo e progressão de recuperação |

Marcadores: `tests/conftest.py` aplica `@pytest.mark.unit` a ficheiros sob `tests/unit/`.
