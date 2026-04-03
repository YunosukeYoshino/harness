import type { Todo } from "./todo";

export interface TodoRepository {
  list(): Promise<Todo[]>;
  create(input: Pick<Todo, "title">): Promise<Todo>;
}
