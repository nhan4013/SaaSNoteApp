import { Navigate } from "react-router-dom";
import type { ProtectedRouteProps } from "../type/types";

function ProtectedRouteProps({children,isAuthenticated,redirectTo}:ProtectedRouteProps){
    return isAuthenticated ? (
        children
    ): (
        <Navigate to={redirectTo} replace />
    )

}

export default ProtectedRouteProps