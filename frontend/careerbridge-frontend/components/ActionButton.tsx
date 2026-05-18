import type { ButtonHTMLAttributes, ReactNode } from "react";

type ActionButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  pending?: boolean;
  pendingLabel?: ReactNode;
};

export default function ActionButton({
  children,
  className = "",
  disabled,
  pending = false,
  pendingLabel = "Working...",
  type = "button",
  ...props
}: ActionButtonProps) {
  return (
    <button
      {...props}
      type={type}
      disabled={disabled || pending}
      aria-busy={pending}
      className={`${className} transition hover:brightness-110 active:scale-[0.99] disabled:cursor-wait disabled:opacity-70`}
    >
      {pending ? pendingLabel : children}
    </button>
  );
}
