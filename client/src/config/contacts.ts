export interface Contacts {
  email: string;
  tel: string;
  telFormatted: string;
}

export const contacts: Contacts = {
  email:        process.env.NEXT_PUBLIC_CONTACT_EMAIL         || "help@drtechno.ru",
  tel:          process.env.NEXT_PUBLIC_CONTACT_TEL           || "+74952152070",
  telFormatted: process.env.NEXT_PUBLIC_CONTACT_TEL_FORMATTED || "+7 (495) 215-20-70",
};