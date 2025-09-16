"use client";

import { motion } from "framer-motion";
import Image from "next/image";

export default function Feature() {
  return (
    <section className="flex flex-col md:flex-row items-center justify-between w-full max-w-6xl mx-auto py-20 px-6">
      {/* 설명 (왼쪽) */}
      <motion.div
        className="flex-1 text-left"
        initial={{ opacity: 0, x: -50 }}
        whileInView={{ opacity: 1, x: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 1 }}
      >
        <h3 className="text-3xl md:text-5xl font-bold mb-6">
          손글씨를 업로드하세요
        </h3>
        <p className="text-lg text-gray-600 leading-relaxed">
          제공된 템플릿에 글씨를 작성한 후 스캔하거나 사진으로 찍어 업로드하면,
          <br />
          AI가 글자의 패턴을 분석해 고유한 폰트 데이터를 생성합니다.
        </p>
      </motion.div>

      {/* 이미지 (오른쪽) */}
      <motion.div
        className="flex-1 mt-10 md:mt-0 md:ml-12"
        initial={{ opacity: 0, x: 50 }}
        whileInView={{ opacity: 1, x: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 1 }}
      >
        <Image
          src="/upload-demo.png" // 👉 public/upload-demo.png 준비 필요
          alt="Upload demo"
          width={500}
          height={400}
          className="rounded-xl shadow-lg"
        />
      </motion.div>
    </section>
  );
}
