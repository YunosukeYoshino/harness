import type { Todo, TodoRepository } from "@repo/domain";

/**
 * Template placeholder.
 * Wire Prisma Client here when you switch from in-memory to DB-backed runtime.
 */
export class PrismaTodoRepository implements TodoRepository {
  async list(): Promise<Todo[]> {
    throw new Error("Not implemented. Add Prisma Client wiring first.");
  }

  async create(_input: Pick<Todo, "title">): Promise<Todo> {
    throw new Error("Not implemented. Add Prisma Client wiring first.");
  }
}
