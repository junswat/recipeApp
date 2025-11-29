import React from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Pagination } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';

export default function SlideView({ steps }) {
    return (
        <div className="slide-view">
            <Swiper
                modules={[Navigation, Pagination]}
                spaceBetween={20}
                slidesPerView={1}
                navigation
                pagination={{ clickable: true }}
                className="mySwiper"
            >
                {steps.map((step, index) => (
                    <SwiperSlide key={index}>
                        <div className="slide-card">
                            <div className="slide-image">
                                {step.image_url ? (
                                    <img src={`http://localhost:8000${step.image_url}`} alt={`Step ${index + 1}`} />
                                ) : (
                                    <div className="no-image">No Image</div>
                                )}
                            </div>
                            <div className="slide-content">
                                <h3>Step {index + 1}</h3>
                                <p>{step.description}</p>
                            </div>
                        </div>
                    </SwiperSlide>
                ))}
            </Swiper>
        </div>
    );
}
