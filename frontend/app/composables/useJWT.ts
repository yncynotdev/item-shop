export default function useJWT() {
  return useState<string | null>("jwt");
}
