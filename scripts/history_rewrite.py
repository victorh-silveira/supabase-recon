
import subprocess
import os

def run_command(command, cwd=None):
    # Set SKIP to bypass pre-commit hooks
    env = os.environ.copy()
    env["SKIP"] = "lint,test,security,commitlint,cleanup"
    result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd, env=env)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(result.stderr)
        return None
    return result.stdout.strip()

def main():
    repo_path = os.getcwd()
    
    # 1. Get all commits in reverse order
    log = run_command('git log --format="%H %s" --reverse', repo_path)
    if not log:
        return
    
    commits = []
    for line in log.split("\n"):
        parts = line.split(" ", 1)
        if len(parts) == 2:
            commits.append({"hash": parts[0], "msg": parts[1]})

    # 2. Define the new structure
    new_messages_by_index = {
        5: "build(repo): configurar ambiente de desenvolvimento e dependencias",
        6: "ci(all): implementar hooks de pre-commit e workflows do github actions",
        7: "docs(all): adicionar documentacao tecnica e guia de arquitetura",
        8: "style(repo): inicializar arvore de diretorios com arquivos gitkeep",
        9: "feat(domain): implementar logica central de parsing e cliente http",
        10: "feat(app): implementar casos de uso e camada de apresentacao cli",
        11: "test(all): adicionar testes unitarios com 100% de cobertura",
        12: "refactor(repo): migrar script procedural para arquitetura ddd",
        13: "refactor(repo): remover script legado apos migracao para ddd",
        14: "docs(all): atualizar guia de arquitetura e documentacao principal",
        15: "feat(domain): refinar logica de extração de bundle e geracao de swagger",
        16: "feat(cli): aprimorar interface visual e telemetria de analise",
        17: "test(all): garantir 100 porcento de cobertura em todas as camadas",
        18: "ci(all): adicionar gitleaks e refinar configuracao de release",
        19: "chore(tools): atualizar script de limpeza do ambiente",
        20: "test(all): refinar validacoes de casos de borda nos testes unitarios",
        21: "fix(ci): restaurar configuracao de release funcional",
        22: "style(repo): persistir pasta raiz de testes no git",
        23: "chore(release): 1.0.0 [skip ci]",
        24: "refactor(tools): centraliza fluxos do pre-commit e expande script de limpeza",
        25: "chore(release): 1.0.1 [skip ci]",
        26: "refactor(tools): remover CVE-2026-3219 das vulnerabilidades ignoradas no script clean_workspace"
    }

    # 3. Start rewriting
    print("Starting history rewrite...")
    
    # Create an orphan branch for the new history
    run_command("git checkout --orphan main-new", repo_path)
    run_command("git reset --hard", repo_path)
    
    hash_map = {} # old_hash -> new_hash

    # Apply initial squash
    initial_commits_hashes = [c["hash"] for c in commits[:5]]
    print("Applying initial squash...")
    run_command(f"git checkout {initial_commits_hashes[-1]} -- .", repo_path)
    run_command("git add .", repo_path)
    run_command('git commit --no-verify -m "feat(repo): inicializar estrutura base do projeto"', repo_path)
    new_initial_hash = run_command("git rev-parse HEAD", repo_path)
    if new_initial_hash:
        for h in initial_commits_hashes:
            hash_map[h] = new_initial_hash
            hash_map[h[:7]] = new_initial_hash[:7]

    # Cherry-pick the rest
    for i in range(5, len(commits)):
        old_hash = commits[i]["hash"]
        msg = new_messages_by_index.get(i, commits[i]["msg"])
        print(f"Cherry-picking {old_hash} as '{msg}'")
        
        # Cherry-pick without committing to amend the message
        run_command(f"git cherry-pick -n {old_hash}", repo_path)
        run_command(f'git commit --no-verify -m "{msg}"', repo_path)
        new_hash = run_command("git rev-parse HEAD", repo_path)
        if new_hash:
            hash_map[old_hash] = new_hash
            hash_map[old_hash[:7]] = new_hash[:7]

    # 4. Update CHANGELOG.md
    print("Updating CHANGELOG.md hashes...")
    changelog_path = os.path.join(repo_path, "docs", "CHANGELOG.md")
    if os.path.exists(changelog_path):
        with open(changelog_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Sort keys by length descending to avoid partial replacements
        sorted_hashes = sorted(hash_map.keys(), key=len, reverse=True)
        for old_h in sorted_hashes:
            content = content.replace(old_h, hash_map[old_h])
            
        with open(changelog_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        run_command("git add docs/CHANGELOG.md", repo_path)
        run_command('git commit --amend --no-edit --no-verify', repo_path)

    print("History rewrite complete.")
    print("To finalize, run:")
    print("git checkout main")
    print("git reset --hard main-new")
    print("git branch -D main-new")
    print("git push origin main --force")

if __name__ == "__main__":
    main()
