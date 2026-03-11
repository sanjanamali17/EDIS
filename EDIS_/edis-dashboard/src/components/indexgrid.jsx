import IndexCard from "./IndexCard";

export default function IndexGrid({ indices }) {
  return (
    <div className="grid">
      {Object.entries(indices).map(([key, val]) => (
        <IndexCard
          key={key}
          name={key.replace("_", " ").toUpperCase()}
          value={val.value}
          status={val.status}
        />
      ))}
    </div>
  );
}
