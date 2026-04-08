import React from "react";

import TopProductsCarousel from "@/components/TopProductsCarousel";
import BrandsCarousel from "@/components/BrandsCarousel";
import Modal from "@/components/Modal";


export default function MainPage() {
  const ListItem = ({ children, highlight }: {children: React.ReactNode; highlight: string}) => (
    <li>
      <span className="text-gray-800 bg-blue-200 p-1 rounded-md">
        { highlight }
      </span>
      { children }
    </li>
  );
  
  return (
    <div className="my-container">
      <div className="brands mb-10">
        <div className="name">
          <h2 className="mb-3">
            Бренды
          </h2>
        </div>
        <BrandsCarousel />
      </div>
      <div className="top mb-10">
        <div className="name">
          <h2 className="mb-3">
            Лидеры продаж
          </h2>
        </div>
        <TopProductsCarousel />
      </div>
      <div className="new-items"></div>
      <div className="description">
        <h5 className="font-bold">
          Доброе утро, добрый день, вечер, а кому-то и доброй ночи! Здравствуйте! Привет всем!!!
        </h5>
        <p className="mb-2">
          Мы рады приветствовать Вас на страницах нашего интернет-магазина! Вся наша дружная команда убеждена в том, что знакомство с нами добавит в вашу жизнь, и так насыщенную яркими моментами, еще больше радостных впечатлений и приятных мгновений, а покупки, сделанные у нас, будут вызывать у вас только самые положительные эмоции. Мы прикладываем максимум наших усилий для того, чтобы вы чувствовали себя комфортно во всем - в удобстве выбора товара, его качестве, качестве нашей доставки, гарантии сервисного обслуживания. Наши основные принципы:
        </p>
        <ul className="list-disc w-[96%] ml-auto flex flex-col gap-1.5">
            <ListItem highlight="*Быстро*" children=" - никакого нудного ожидания. Все по делу и вовремя" />
            <ListItem highlight="*Точно*" children=" - процесс сборки заказа контролируется на всех этапах" />
            <ListItem highlight="*Профессионально*" children=" - наш менеджер поможет выбрать нужный гаджет исходя из Ваших потребностей" />
            <ListItem highlight="*Хамству бой*" children=" - постоянный контроль за работой операторов" />
            <ListItem highlight="*Доставка*" children=" - всегда точно в срок" />
        </ul>
        <Modal />
      </div>
    </div>
  )
}


