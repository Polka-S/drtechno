"use client";
import React, { useRef, useState } from "react";
import { X } from "lucide-react";
import { useForm, SubmitHandler } from "react-hook-form";

import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { closeAuthModal } from "@/store/slices/uiSlice";
import { login, register } from '@/store/slices/authSlice';
import IconButton from "@/components/IconButton";
import AuthForm, { FormValues } from "@/components/AuthForm";


const Modal = () => {
  const dispatch = useAppDispatch();
  const isOpen = useAppSelector((state) => state.ui.isAuthOpen);
  const modalRef = useRef<HTMLDivElement>(null);
  const isLoading = useAppSelector((state) => state.auth.isLoading)
  const [mode, setMode] = useState<"login" | "register">("login");

  const handleAuth = async (data: FormValues) => {
    if (mode === 'login') {
      const res = await dispatch(login({email: data.email, password: data.password}));

      if (login.fulfilled.match(res)) dispatch(closeAuthModal());
    } else {
      if (!data.name) return;

      const res = await dispatch(register({
        name: data.name,
        email: data.email,
        password: data.password,
      }));

      if (register.fulfilled.match(res)) dispatch(closeAuthModal());
    }
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    if (modalRef.current?.contains(e.target as Node)) return;

    (e.currentTarget as HTMLDivElement).dataset.shouldClose = "true";
  }

  const handleMouseUp = (e: React.MouseEvent) => {
    const target = e.currentTarget as HTMLDivElement;

    if (target.dataset.shouldClose === "true" && !modalRef.current?.contains(e.target as Node))
      dispatch(closeAuthModal());

    delete target.dataset.shouldClose;
  }

  if (!isOpen) return null;

  return (
    <>
    <div
      onMouseDown={(e) => handleMouseDown(e)}
      onMouseUp={(e) => handleMouseUp(e)}
      className={`
        fixed inset-0 z-20 flex items-center justify-center
      bg-gray-900/60 backdrop-blur-sm
        transition-all duration-300 ease-out
        ${isOpen ? 'opacity-100 visible' : 'opacity-0 invisible'}
      `}
    >
      <div
        ref={modalRef}
        onClick={(e) => e.stopPropagation()}
        className={`
          modal-content relative bg-white rounded-2xl shadow-2xl
          p-6 w-full max-w-md transform transition-all duration-300
          ${isOpen ? 'scale-100 opacity-100' : 'scale-95 opacity-0'}
        `}
      >
        <IconButton icon={X} onClick={() => dispatch(closeAuthModal())} className="absolute top-1.5 right-1.5" />
        <div className="mt-4 text-center text-sm">
          <AuthForm mode={mode} onSubmit={handleAuth} isLoading={isLoading} />
          <div className="change-mode mt-2">
            {mode === "login" ? (
              <>
                Нет аккаунта?{" "}
                <button onClick={() => setMode("register")} className="text-blue-600">
                  Зарегистрироваться
                </button>
              </>
            ) : (
              <>
                Уже есть аккаунт?{" "}
                <button onClick={() => setMode("login")} className="text-blue-600">
                  Войти
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
    </>
  );
};

export default Modal;