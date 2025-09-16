import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const formData = await req.formData();
  const file = formData.get("file") as File;

  const backend = "http://localhost:8000/analyze";
  const uploadForm = new FormData();
  uploadForm.append("file", file);

  const res = await fetch(backend, {
    method: "POST",
    body: uploadForm,
  });

  const data = await res.json();
  return NextResponse.json(data);
}
