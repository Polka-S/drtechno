import { createSlice } from "@reduxjs/toolkit";


interface UIState {
  isAuthOpen: boolean;
}

const initialState: UIState = {
  isAuthOpen: false,
};

const uiSlice = createSlice({
  name: "ui",
  initialState,
  reducers: {
    openAuthModal: (state) => {
      state.isAuthOpen = true;
    },
    closeAuthModal: (state) => {
      state.isAuthOpen = false;
    },
    toggleAuthModal: (state) => {
      state.isAuthOpen = !state.isAuthOpen;
    },
  }
});

export const { openAuthModal, closeAuthModal, toggleAuthModal } = uiSlice.actions;
export default uiSlice.reducer;