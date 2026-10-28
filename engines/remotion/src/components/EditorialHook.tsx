import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface EditorialHookProps {
  eyebrow?: string;
  headline: string;
  subhead?: string;
  primaryColor?: string;
  highlightColor?: string;
}

export const EditorialHook: React.FC<EditorialHookProps> = ({
  eyebrow = "INSIGHT",
  headline = "QUAY 1 LẦN DỰNG ĐA KÊNH",
  subhead = "SUPER STUDIO OMNI-FLOW v4.0",
  primaryColor = "#F2EDE4",
  highlightColor = "#720000",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame,
    fps,
    config: { damping: 12, mass: 0.5, stiffness: 100 },
  });

  const opacity = interpolate(frame, [0, 10], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        top: 280,
        left: 60,
        right: 60,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        textAlign: "center",
        transform: `scale(${scale})`,
        opacity,
        fontFamily: "'Playfair Display', serif",
      }}
    >
      {eyebrow && (
        <span
          style={{
            fontSize: 28,
            letterSpacing: 4,
            textTransform: "uppercase",
            color: highlightColor,
            fontWeight: 700,
            marginBottom: 12,
            fontFamily: "'Be Vietnam Pro', sans-serif",
          }}
        >
          {eyebrow}
        </span>
      )}
      <h1
        style={{
          fontSize: 64,
          lineHeight: 1.15,
          color: primaryColor,
          margin: 0,
          textShadow: "0 8px 32px rgba(0,0,0,0.6)",
        }}
      >
        {headline}
      </h1>
      {subhead && (
        <p
          style={{
            fontSize: 32,
            color: primaryColor,
            opacity: 0.9,
            marginTop: 16,
            fontFamily: "'Be Vietnam Pro', sans-serif",
          }}
        >
          {subhead}
        </p>
      )}
    </div>
  );
};
