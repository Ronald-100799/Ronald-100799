import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import { ThreeCanvas } from "@remotion/three";

// A barbell that loads one plate per side at a time: "add a little each week".
export const plateLoadSchema = {
  plates: 3,
  hotColor: "#FFE11A",
  plateColor: "#1c1c20",
};
type Props = typeof plateLoadSchema;

const Plate: React.FC<{ x: number; r: number; color: string; enter: number }> = ({ x, r, color, enter }) => {
  const side = Math.sign(x);
  const from = x + side * 2.2;
  return (
    <group position={[interpolate(enter, [0, 1], [from, x]), 0, 0]} scale={Math.max(enter, 0.001)}>
      <mesh rotation={[0, 0, Math.PI / 2]}>
        <cylinderGeometry args={[r, r, 0.16, 64]} />
        <meshStandardMaterial color={color} roughness={0.5} metalness={0.2} />
      </mesh>
    </group>
  );
};

export const PlateLoad: React.FC<Props> = ({ plates, hotColor, plateColor }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const intro = spring({ frame, fps, config: { damping: 14 } });
  const turn = interpolate(frame, [0, 105], [-0.7, 0.35], { easing: Easing.inOut(Easing.sin) });
  const list = Array.from({ length: plates }, (_, i) => i);
  return (
    <ThreeCanvas width={width} height={height} camera={{ position: [0, 0.9, 8.6], fov: 32 }} gl={{ alpha: true }}>
      <hemisphereLight args={["#ffffff", "#202028", 1.6]} />
      <directionalLight position={[3, 4, 5]} intensity={2.4} color="#fff1d6" />
      <directionalLight position={[-4, 2, -3]} intensity={1.4} color="#9fc4ff" />
      <group rotation={[0.25, turn, -0.08]} scale={intro}>
        <mesh rotation={[0, 0, Math.PI / 2]}>
          <cylinderGeometry args={[0.07, 0.07, 3.6, 32]} />
          <meshStandardMaterial color="#8a8f99" roughness={0.3} metalness={0.85} />
        </mesh>
        {list.flatMap((i) => {
          const enter = spring({ frame: frame - 18 - i * 16, fps, config: { damping: 13 } });
          const last = i === plates - 1;
          const r = 0.78 - i * 0.12;
          return [-1, 1].map((s) => (
            <Plate key={`${i}${s}`} x={s * (0.75 + i * 0.18)} r={r} color={last ? hotColor : plateColor} enter={enter} />
          ));
        })}
      </group>
    </ThreeCanvas>
  );
};
