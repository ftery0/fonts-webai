"use client";

import { useState } from "react";

export default function UploadForm() {
  const [file, setFile] = useState<File | null>(null);
  const [lang, setLang] = useState<"kor" | "eng">("kor");
  const [result, setResult] = useState<Record<string, unknown> | null>(null);


  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    formData.append("lang", lang);

    const res = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setResult(data);
  };

  return (
    <div className="p-6 border rounded-xl shadow-md bg-gray-50 w-full max-w-md">
      <label className="block mb-2 font-medium">언어 선택</label>
      <select
        value={lang}
        onChange={(e) => setLang(e.target.value as "kor" | "eng")}
        className="w-full mb-4 p-2 border rounded"
      >
        <option value="kor">한글</option>
        <option value="eng">영어</option>
      </select>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="mb-4"
      />

      <button
        onClick={handleUpload}
        className="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        업로드
      </button>

      {result && (
        <pre className="mt-4 p-2 bg-white border rounded text-sm">
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  );
}
