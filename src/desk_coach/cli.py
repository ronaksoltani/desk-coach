import argparse
import time

from plyer import notification

from .posture import check_camera


def _remind(interval_minutes: int, duration_minutes: int) -> None:
    deadline = time.monotonic() + duration_minutes * 60
    next_reminder = time.monotonic() + interval_minutes * 60
    print("Desk Coach is running. Press Ctrl+C to stop.")
    while time.monotonic() < deadline:
        remaining = min(next_reminder - time.monotonic(), deadline - time.monotonic())
        if remaining > 0:
            time.sleep(remaining)
        if time.monotonic() >= next_reminder and time.monotonic() < deadline:
            try:
                notification.notify(title="Desk Coach", message="Drink some water and take a short stretch break.", timeout=10)
            except Exception:
                print("Reminder: drink water and stretch.")
            next_reminder += interval_minutes * 60


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Local hydration reminders and optional camera hint.")
    commands = parser.add_subparsers(dest="command", required=True)
    remind = commands.add_parser("remind")
    remind.add_argument("--interval", type=int, default=60, help="minutes between reminders")
    remind.add_argument("--duration", type=int, default=480, help="minutes to keep reminders active")
    camera = commands.add_parser("camera-check", help="capture one frame for a rough proximity hint")
    camera.add_argument("--index", type=int, default=0)
    args = parser.parse_args(argv)
    if args.command == "remind":
        if args.interval <= 0 or args.duration <= 0:
            parser.error("interval and duration must be positive")
        try:
            _remind(args.interval, args.duration)
        except KeyboardInterrupt:
            print("\nDesk Coach stopped.")
    else:
        try:
            result = check_camera(args.index)
        except (RuntimeError, ImportError) as error:
            parser.error(str(error) + " (install with pip install desk-coach[camera])")
        if not result.face_detected:
            print("No face detected; no image was saved.")
        elif result.too_close:
            print(f"You may be close to the camera (face width {result.face_width_ratio:.0%}); consider sitting back.")
        else:
            print("Face detected at a typical camera distance.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
