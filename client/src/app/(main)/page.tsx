import Carousel from "@/components/Carousel";

export default function MainPage() {
  return (
    
    <div className="my-container">
      <div className="top">
        <div className="name">
          <h2 className="mb-3">
            Лидеры продаж
          </h2>
        </div>
        <Carousel />
      </div>
      <div className="new-items"></div>
    </div>
  )
}