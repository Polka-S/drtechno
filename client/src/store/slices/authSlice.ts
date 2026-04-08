import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";

import { User } from '@/types/user';


interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
}

export const fetchCurrentUser = createAsyncThunk(
  'auth/fetchCurrentUser',
  async () => {
    const res = await fetch('/api/auth/me', {credentials: 'include'});
    if (!res.ok) throw new Error(`Not authenticated: ${res.status}`)
    return (await res.json() as User)
  }
)

export const register = createAsyncThunk(
  'auth/register',
  async ({
    email,
    password,
    name,
  }: { email: string; password: string, name: string}) => {
    const res = await fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, name }),
      credentials: 'include',
    })

    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.detail || 'Registration failed')
    }

    return (await res.json() as User);
  }
)

export const login = createAsyncThunk(
  'auth/login',
  async ({
    email,
    password
  }: {email: string; password: string}) => {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
      credentials: 'include',
    });
    
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.detail || "Login failed");
    }

    return (await res.json() as User);
  }
)

export const logout = createAsyncThunk(
  'auth/logout',
  async () => {
    await fetch('/api/auth/logout', { method: 'POST', credentials: 'include' });
  }
);

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(
        fetchCurrentUser.fulfilled,
        (state, action: PayloadAction<User>) => {
          state.user = action.payload;
          state.isAuthenticated = true;
          state.isLoading = false;
        }
      )
      .addCase(
        fetchCurrentUser.rejected,
        (state) => {
          state.user = null;
          state.isAuthenticated = false;
          state.isLoading = false;
        }
      )
      .addCase(
        fetchCurrentUser.pending,
        (state) => {
          state.isLoading = true;
        }
      )
      // login
      .addCase(
        login.fulfilled,
        (state, action: PayloadAction<User>) => {
          state.user = action.payload;
          state.isAuthenticated = true;
          state.isLoading = false;
          state.error = null;
        }
      )
      .addCase(
        login.rejected,
        (state, action) => {
          state.isAuthenticated = false;
          state.isLoading = false;
          state.error = action.error.message ?? 'Login failed';
        }
      )
      .addCase(
        login.pending,
        (state) => {
          state.isLoading = true;
          state.error = null;
        }
      )
      // logout
      .addCase(
        logout.fulfilled,
        (state) => {
          state.isAuthenticated = false;
          state.user = null
        }
      )
      // register
      .addCase(
        register.fulfilled,
        (state, action: PayloadAction<User>) => {
          state.user = action.payload;
          state.isAuthenticated = true;
          state.isLoading = false;
        }
      )
      .addCase(
        register.rejected,
        (state, action) => {
          state.isLoading = false;
          state.error = action.error.message ?? 'Registration failed';
        }
      )
      .addCase(
        register.pending,
        (state) => {
          state.isLoading = true;
          state.error = null;
        }
      );
  },
});

export const { clearError } = authSlice.actions;
export default authSlice.reducer;