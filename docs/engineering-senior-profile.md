# Perfil Sênior de Engenharia e Postura Técnica

Diretrizes de maturidade técnica, rigor metodológico e postura profissional esperada no desenvolvimento do **Supabase Recon**.

---

## 1. Princípios de Atuação

1. **Autonomia com Governança**:
   - Diagnosticar causas raízes antes de propor alterações.
   - Compreender os impactos em cascata na arquitetura antes de introduzir novas dependências ou abstrações.
2. **Defesa em Profundidade**:
   - Considerar todo input externo (URLs, bundles JS compilados, respostas de rede) como potencialmente malicioso ou inconsistente.
   - Tratar falhas de forma resiliente, assegurando códigos de retorno semânticos e mensagens claras.
3. **Simplicidade Radical**:
   - Evitar sobre-engenharia. A melhor solução é a mais simples, fortemente tipada, estritamente testada e contida em menos de 300 linhas por arquivo.

---

## 2. Invariantes de Entrega

- Nunca marcar uma tarefa como concluída sem execução e evidência objetiva de aprovação em testes.
- Manter a cobertura de branches em **100%** de forma contínua.
- Respeitar a divisão e pureza das camadas do DDD Hexagonal.
