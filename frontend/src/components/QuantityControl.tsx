interface QuantityControlProps {
  value: number;
  onChange: (value: number) => void;
  min?: number;
  max?: number;
}

export function QuantityControl({ value, onChange, min = 1, max }: QuantityControlProps) {
  const handleDecrement = () => {
    if (value > min) {
      onChange(value - 1);
    }
  };

  const handleIncrement = () => {
    if (!max || value < max) {
      onChange(value + 1);
    }
  };

  return (
    <div className="flex items-center border-2 border-gray-300 rounded-lg overflow-hidden">
      <button
        onClick={handleDecrement}
        disabled={value <= min}
        className="px-5 py-3 bg-white border-none cursor-pointer text-xl text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        aria-label="Decrease quantity"
      >
        −
      </button>
      <span className="px-6 py-3 font-semibold text-gray-900">{value}</span>
      <button
        onClick={handleIncrement}
        disabled={!!max && value >= max}
        className="px-5 py-3 bg-white border-none cursor-pointer text-xl text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        aria-label="Increase quantity"
      >
        +
      </button>
    </div>
  );
}
