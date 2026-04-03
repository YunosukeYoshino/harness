import type { TodoRepository } from "@repo/domain";

export async function listTodos(repo: TodoRepository) {
  return repo.list();
}
