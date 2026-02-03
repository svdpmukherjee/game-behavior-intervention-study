const CoinIcon = ({ className }) => (
  <svg viewBox="0 0 24 24" className={className} fill="currentColor">
    {/* Outer ring with shine effect */}
    <circle cx="12" cy="12" r="11" fill="currentColor" opacity="0.1" />
    <circle cx="12" cy="12" r="10" fill="currentColor" opacity="0.2" />
    <circle
      cx="12"
      cy="12"
      r="10"
      stroke="currentColor"
      strokeWidth="1.5"
      fill="none"
    />

    {/* Shine effect */}
    <path
      d="M12 2C17.52 2 22 6.48 22 12"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      opacity="0.5"
    />

    {/* Inner details */}
    <circle
      cx="12"
      cy="12"
      r="7"
      stroke="currentColor"
      strokeWidth="1"
      fill="none"
      opacity="0.3"
    />

    {/* 'p' text */}
    <text
      x="12"
      y="14"
      fontSize="8"
      textAnchor="middle"
      fill="currentColor"
      fontWeight="bold"
    >
      p
    </text>
  </svg>
);
export default CoinIcon;
