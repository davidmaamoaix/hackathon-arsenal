using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MovementController: MonoBehaviour {
    // Note: the following code does not follow C#'s recommended
    // coding style; you might want to change that in your own
    // project (unless you are like me, and cannot stand Microsoft's
    // absurd coding conventions).

    // Movement constants.
    private const float GRAVITY = 0.005F;
    private const float MAX_FALL = -0.75F;
    private const float SPEED = 5F;
    private const float JUMP_FORCE = 0.3F;
    private const float VROT_RANGE = 90;
    private const float MOUSE_SEN = 5;

    // SerializeFields.
    [SerializeField]
    private CharacterController controller;
    [SerializeField]
    private GameObject cam;

    // Player attributes.
    private float vSpeed;
    private float jumpForce;
    private float vRot;

    // Public player attributes.
    public Vector3 extraForce { get; private set; }
    public float velocity { get; private set; }
    public float maxSpeed;

    void Start() {
        this.extraForce = Vector3.zero;
        Cursor.lockState = CursorLockMode.Locked;
    }

    void Update() {

        // Basic movements.
        float hMove = Input.GetAxis("Horizontal");
        float vMove = Input.GetAxis("Vertical");
        Vector3 move = new Vector3(hMove * SPEED, 0, vMove * SPEED);

        this.handleMouse();
        this.tickMovement(move);

        if (Input.GetKeyDown(KeyCode.P)) {
            this.addForce(20, 0.25F, 20);
        }
    }

    private void handleMouse() {

        // Horizontal rotation (player).
        float mouseHorizontal = Input.GetAxis("Mouse X") * MOUSE_SEN;
        this.transform.Rotate(0, mouseHorizontal, 0);

        // Vertical rotation (camera).
        this.vRot -= Input.GetAxis("Mouse Y") * MOUSE_SEN;
        this.vRot = Mathf.Clamp(this.vRot, -VROT_RANGE, VROT_RANGE);
        this.cam.transform.localRotation = Quaternion.Euler(this.vRot, 0, 0);
    }

    private void tickMovement(Vector3 move) {

        // Jumping & gravity.
        if (this.controller.isGrounded) {
            if (Input.GetButton("Jump")) {
                this.jumpForce = JUMP_FORCE;
            }
            this.vSpeed = Mathf.Max(0, this.vSpeed);
        } else {
            if (this.jumpForce < 0.001F) {
                this.vSpeed = Mathf.Max(MAX_FALL, this.vSpeed - GRAVITY);
            }
        }

        float moveMagnitude = move.magnitude;
        if (moveMagnitude > this.maxSpeed) {
            move *= this.maxSpeed / moveMagnitude;
        }

        if (!this.controller.isGrounded) {
            move *= 0.5F;
        }
        move = this.transform.rotation * move;

        // Jump force decay & applying to movement.
        this.vSpeed += this.jumpForce / 2.5F;
        move.y = this.vSpeed * 45F;
        if ((this.jumpForce *= 0.5F) < 0.2F) {
            this.jumpForce = 0;
        }

        // Extra force handling.
        float extraForceMagnitude = this.extraForce.magnitude;

        if (extraForceMagnitude < 0.01F) {
            this.extraForce = Vector3.zero;
        }

        this.extraForce *= 0.95F;

        this.velocity = move.magnitude + extraForceMagnitude;

        // Actual moving.
        move += this.extraForce;
        move *= Time.deltaTime;
        controller.Move(move);
    }

    public void addForce(Vector3 velocity) {
        this.jumpForce += velocity.y;
        velocity.y = 0;
        this.extraForce += velocity;
    }

    public void addForce(float x, float y, float z) {
        this.addForce(new Vector3(x, y, z));
    }
}
