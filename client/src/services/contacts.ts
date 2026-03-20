import { contacts as localContacts, type Contacts } from "@/config/contacts";


export async function getContacts(): Promise<Contacts> {
  return localContacts;
}