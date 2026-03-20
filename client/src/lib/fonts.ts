import { Roboto, Poppins } from "next/font/google";


export const roboto = Roboto({
  variable: "--font-roboto-sans",
  subsets: ["latin"],
});

export const poppins = Poppins({
  weight: ["100", "200", "600", "700"],
  variable: "--font-poppins-sans",
  subsets: ["latin"]
});