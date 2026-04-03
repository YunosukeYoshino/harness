import type { Todo, TodoRepository } from "@repo/domain";

export class InMemoryTodoRepository implements TodoRepository {
  #items: Todo[] = [];

  async list() {
    return this.#items;
  }

  async create(input: Pick<Todo, "title">) {
    const item: Todo = {
      id: crypto.randomUUID(),
      title: input.title,
      completed: false,
      createdAt: new Date().toISOString(),
    };
    this.#items.push(item);
    return item;
  }
}
