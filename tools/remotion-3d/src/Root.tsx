import React from "react";
import { Composition } from "remotion";
import { PlateLoad, plateLoadSchema } from "./PlateLoad";
import { PatentUnlock, patentUnlockSchema } from "./PatentUnlock";

// Square, transparent 3D inserts. Size them in the reel with an "overlays" entry.
export const Root: React.FC = () => (
  <>
  <Composition
    id="PlateLoad"
    component={PlateLoad}
    durationInFrames={105}
    fps={30}
    width={1080}
    height={1080}
    defaultProps={plateLoadSchema}
  />

  <Composition
    id="PatentUnlock"
    component={PatentUnlock}
    durationInFrames={66}
    fps={30}
    width={1080}
    height={1080}
    defaultProps={patentUnlockSchema}
  />
  </>
);
