import { Composition } from "remotion";
import { EditorialHook } from "./components/EditorialHook";

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="EditorialHookAlpha"
        component={EditorialHook}
        durationInFrames={150}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          eyebrow: "INSIGHT",
          headline: "QUAY 1 LẦN DỰNG ĐA KÊNH",
          subhead: "SUPER STUDIO OMNI-FLOW v4.0",
        }}
      />
    </>
  );
};
