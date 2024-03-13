import Animal from "./Animal";
import LeftNav from "./LeftNav";

function Animals() {
  return (
    <div className="flex flex-row h-main">
      <div className="w-40">
        <LeftNav />
      </div>
      <div className="mx-auto pt-8">
        <Animal />
      </div>
    </div>
  );
}

export default Animals;

