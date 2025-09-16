"use client";
import { useState } from "react";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null)
  const [fontUrl, setFontUrl] = useState("")

  const handleUpload = async () => {
    if (!file) return
    const formData = new FormData()
    formData.append("file", file)

    const res = await fetch("/api/upload", { method: "POST", body: formData })
    const data = await res.json()
    setFontUrl(data.url)
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>손글씨 템플릿 업로드</h1>
      <input type="file" onChange={e => setFile(e.target.files?.[0] || null)} />
      <button onClick={handleUpload} style={{ marginLeft: 10 }}>업로드</button>

      {fontUrl && (
        <div style={{ marginTop: 20 }}>
          <p>폰트 생성 완료! 다운로드:</p>
          <a href={fontUrl} download>다운로드</a>
        </div>
      )}
    </div>
  )
}
