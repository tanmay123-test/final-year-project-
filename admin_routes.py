
# ================= ADMIN ROUTES =================
@app.route("/admin/workers/pending")
def admin_pending_workers():
    workers = worker_db.get_pending_workers()
    return jsonify(workers), 200


@app.route("/admin/worker/approve/<int:worker_id>", methods=["POST"])
def admin_approve_worker(worker_id):
    worker_db.approve_worker(worker_id)
    return jsonify({"msg": "Worker approved"}), 200


@app.route("/admin/worker/reject/<int:worker_id>", methods=["POST"])
def admin_reject_worker(worker_id):
    worker_db.reject_worker(worker_id)
    return jsonify({"msg": "Worker rejected"}), 200
