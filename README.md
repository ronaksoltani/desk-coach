# Desk Coach

A small desktop reminder for water and stretch breaks, with an optional one-frame webcam check that estimates whether a detected face is unusually close to the camera. The camera is opened only when you run the explicit `camera-check` command.

## Quick start

```bash
python -m venv .venv
python -m pip install -e .
desk-coach remind --interval 60 --duration 480
desk-coach camera-check
```

`camera-check` may trigger an operating-system camera permission prompt. The program processes one frame in memory, prints a rough proximity hint, then releases the camera. It does not save or transmit images. Haar-cascade face detection is not posture measurement or medical advice; lighting, camera placement, and individual faces affect the estimate.

## Learning notes

Practice a small subcommand CLI, timed scheduling, native notifications, and the lifecycle of an OpenCV camera resource (`open`, `read`, `release`).

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

## License

MIT. See [LICENSE](LICENSE).
