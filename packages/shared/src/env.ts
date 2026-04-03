export function requiredEnv(name: string, value = process.env[name]) {
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}
