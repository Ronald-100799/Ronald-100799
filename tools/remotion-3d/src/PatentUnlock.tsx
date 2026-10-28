import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import { ThreeCanvas } from "@remotion/three";

// A padlock drops in, the shackle springs open, and the lock falls away: "the patent is off".
export const patentUnlockSchema = { color: "#E10600", metal: "#e4e6ea" };
type Props = typeof patentUnlockSchema;

export const PatentUnlock: React.FC<Props> = ({ color, metal }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const drop = spring({ frame, fps, config: { damping: 11, stiffness: 140 } });
  const open = spring({ frame: frame - 20, fps, config: { damping: 9, stiffness: 160 } });
  const fall = interpolate(frame, [40, 62], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.in(Easing.cubic) });
  const shake = frame >= 18 && frame < 22 ? Math.sin(frame * 3.1) * 0.06 : 0;
  return (
    <ThreeCanvas width={width} height={height} camera={{ position: [0, 0.3, 7.5], fov: 34 }} gl={{ alpha: true }}>
      <hemisphereLight args={["#ffffff", "#1a0a0a", 1.5]} />
      <directionalLight position={[3, 4, 5]} intensity={2.6} color="#fff4ea" />
      <directionalLight position={[-4, 1, -3]} intensity={1.6} color="#ff6a5a" />
      <group
        position={[0, interpolate(drop, [0, 1], [3.5, -0.75]) - fall * 4.2, 0]}
        rotation={[0.12, -0.35 + fall * 0.6, shake - fall * 0.9]}
      >
        {/* body */}
        <mesh>
          <boxGeometry args={[1.9, 1.5, 0.7]} />
          <meshStandardMaterial color={color} roughness={0.45} metalness={0.25} />
        </mesh>
        {/* keyhole */}
        <mesh position={[0, 0.08, 0.36]}>
          <cylinderGeometry args={[0.13, 0.13, 0.04, 32]} />
          <meshStandardMaterial color="#111" />
        </mesh>
        <mesh position={[0, -0.18, 0.36]}>
          <boxGeometry args={[0.1, 0.36, 0.04]} />
          <meshStandardMaterial color="#111" />
        </mesh>
        {/* shackle: lifts and swings open around its left leg */}
        <group position={[-0.55, 0.75 + open * 0.45, 0]} rotation={[0, open * -Math.PI * 0.85, 0]}>
          <group position={[0.55, 0, 0]}>
            <mesh position={[0, 0.55, 0]}>
              <torusGeometry args={[0.55, 0.13, 24, 64, Math.PI]} />
              <meshStandardMaterial color={metal} roughness={0.3} metalness={0.55} />
            </mesh>
            {[-0.55, 0.55].map((x) => (
              <mesh key={x} position={[x, 0.2, 0]}>
                <cylinderGeometry args={[0.13, 0.13, 0.7, 24]} />
                <meshStandardMaterial color={metal} roughness={0.3} metalness={0.55} />
              </mesh>
            ))}
          </group>
        </group>
      </group>
    </ThreeCanvas>
  );
};
