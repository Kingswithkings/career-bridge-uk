"use client";

import { useEffect, useRef, useState } from "react";
import {
  FaceLandmarker,
  HandLandmarker,
  FilesetResolver,
} from "@mediapipe/tasks-vision";

export default function BodyLanguageCoachPage() {
  const videoRef = useRef<HTMLVideoElement | null>(null);

  const [faceDetected, setFaceDetected] = useState(false);
  const [handDetected, setHandDetected] = useState(false);
  const [score, setScore] = useState(0);
  const [feedback, setFeedback] = useState("Starting camera...");

  useEffect(() => {
    let faceLandmarker: FaceLandmarker;
    let handLandmarker: HandLandmarker;
    let animationId: number;
    let stream: MediaStream;

    async function setup() {
      const vision = await FilesetResolver.forVisionTasks(
        "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm"
      );

      faceLandmarker = await FaceLandmarker.createFromOptions(vision, {
        baseOptions: {
          modelAssetPath:
            "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task",
          delegate: "GPU",
        },
        runningMode: "VIDEO",
        outputFaceBlendshapes: true,
        numFaces: 1,
      });

      handLandmarker = await HandLandmarker.createFromOptions(vision, {
        baseOptions: {
          modelAssetPath:
            "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task",
          delegate: "GPU",
        },
        runningMode: "VIDEO",
        numHands: 2,
      });

      stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false,
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }

      analyse();
    }

    function analyse() {
      if (!videoRef.current || !faceLandmarker || !handLandmarker) {
        animationId = requestAnimationFrame(analyse);
        return;
      }

      const video = videoRef.current;
      const now = performance.now();

      const faceResult = faceLandmarker.detectForVideo(video, now);
      const handResult = handLandmarker.detectForVideo(video, now);

      const hasFace = faceResult.faceLandmarks.length > 0;
      const hasHand = handResult.landmarks.length > 0;

      setFaceDetected(hasFace);
      setHandDetected(hasHand);

      let currentScore = 0;
      const comments: string[] = [];

      if (hasFace) {
        currentScore += 60;
        comments.push("Face detected clearly.");

        const blendshapes = faceResult.faceBlendshapes?.[0]?.categories || [];

        const smileLeft =
          blendshapes.find((b) => b.categoryName === "mouthSmileLeft")?.score ||
          0;

        const smileRight =
          blendshapes.find((b) => b.categoryName === "mouthSmileRight")?.score ||
          0;

        const smileScore = (smileLeft + smileRight) / 2;

        if (smileScore > 0.25) {
          currentScore += 20;
          comments.push("Positive facial expression detected.");
        } else {
          comments.push("Try to look more relaxed and confident.");
        }
      } else {
        comments.push("Face not visible. Look towards the camera.");
      }

      if (hasHand) {
        currentScore += 10;
        comments.push("Hand movement detected.");
      } else {
        currentScore += 20;
        comments.push("Hand movement is calm.");
      }

      currentScore = Math.min(currentScore, 100);
      setScore(currentScore);

      if (currentScore >= 80) {
        setFeedback("Strong interview presence. " + comments.join(" "));
      } else if (currentScore >= 50) {
        setFeedback("Good start. " + comments.join(" "));
      } else {
        setFeedback("Needs improvement. " + comments.join(" "));
      }

      animationId = requestAnimationFrame(analyse);
    }

    setup().catch((error) => {
      console.error(error);
      setFeedback("Camera or MediaPipe could not start. Check browser permission.");
    });

    return () => {
      cancelAnimationFrame(animationId);
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <div className="mx-auto max-w-5xl">
        <h1 className="text-3xl font-bold text-gray-900">
          AI Interview Body Language Coach
        </h1>

        <p className="mt-2 text-gray-600">
          Practise your interview while CareerBridge analyses face visibility,
          confidence signals, and hand movement.
        </p>

        <div className="mt-6 grid gap-6 md:grid-cols-2">
          <div className="rounded-2xl bg-white p-4 shadow">
            <video
              ref={videoRef}
              className="h-[360px] w-full rounded-xl bg-black object-cover"
              muted
              playsInline
            />
          </div>

          <div className="rounded-2xl bg-white p-6 shadow">
            <h2 className="text-xl font-semibold text-gray-900">
              Live Analysis
            </h2>

            <div className="mt-6 space-y-4 text-gray-800">
              <p>
                Face detected:{" "}
                <span
                  className={
                    faceDetected ? "font-semibold text-green-600" : "font-semibold text-red-600"
                  }
                >
                  {faceDetected ? "Yes" : "No"}
                </span>
              </p>

              <p>
                Hand movement:{" "}
                <span
                  className={
                    handDetected ? "font-semibold text-yellow-600" : "font-semibold text-green-600"
                  }
                >
                  {handDetected ? "Detected" : "Calm / Not detected"}
                </span>
              </p>

              <p className="text-5xl font-bold text-gray-900">{score}/100</p>

              <p className="rounded-xl bg-gray-100 p-4 text-gray-700">
                {feedback}
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}