import type { TodoRepository } from "@repo/domain";

export async function createTodo(repo: TodoRepository, title: string) {
  return repo.create({ title });
}
