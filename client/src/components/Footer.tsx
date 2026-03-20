import Link from "next/link";
import { contacts } from "@/config/contacts";


const Footer = () => {
  const generalColsStyles = "flex flex-col gap-2"
  const generalHrStyles = "text-gray-700"
  const year = new Date().getFullYear()
  
  return (
    <footer className="footer bg-gray-800 text-blue-50">
      <div className="my-container">
        <div className="content">
          <div className="top-content flex flex-col justify-between py-2 gap-10 sm:flex-row sm:items-center">
            <div className={`content-left ${generalColsStyles}`}>
                <h6>Покупателям</h6>
                <hr className={generalHrStyles} />
              <ul className="links-list">
                <li>
                  <Link href="/help">Помощь</Link>
                </li>
                <li>
                  <Link href="/about">О компании</Link>
                </li>
                <li>
                  <Link href="/privacy_policy">Политика конфиденциальности</Link>
                </li>
              </ul>
            </div>
            <div className={`content-right ${generalColsStyles}`}>
              <h6>Оставайтесь на связи</h6>
              <hr className={generalHrStyles} />
              <Link href={`tel:${contacts.tel}`}>
                {contacts.telFormatted}
              </Link>
              <div className="work-time text-sm ">
                <p>ПН-ПТ: 9:00 — 20:00</p>
                <p>СБ-ВС: 10:00 — 18:00</p>
              </div>
              <Link href={`mailto:${contacts.email}`}>{contacts.email}</Link>
            </div>
          </div>
          <hr className={generalHrStyles} />
          <div className="copyright text-right text-sm py-2">
            Copyright 2012-{year} / Все права защищены
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer;