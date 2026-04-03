import { z } from "zod";

export const todoSchema = z.object({
  id: z.string(),
  title: z.string().min(1),
  completed: z.boolean(),
  createdAt: z.string(),
});

export const createTodoInputSchema = z.object({
  title: z.string().min(1),
});
