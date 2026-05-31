from fastapi import APIRouter

from app.controllers.auth import (
    signup,
    login,
    refresh_access_token,
    logout,
    verify_email,
    forgot_password,
    reset_password,
    check_username,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

router.post("/signup")(signup)
router.post("/login")(login)
router.post("/refresh")(refresh_access_token)
router.post("/logout")(logout)
router.get("/verify/{token}")(verify_email)
router.post("/forgot-password")(forgot_password)
router.post("/reset-password")(reset_password)
router.get("/check-username")(check_username)