import { jwtDecode } from 'jwt-decode'

export function isTokenStatus(token: string | null) {
    if (!token) return true;
    try {
        const { exp } = jwtDecode(token) as { exp: number };
        if (exp) {
            return Date.now() >= exp * 1000;
        }
        return true;
    } catch {
        return true;
    }
}