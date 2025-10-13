function ErrorMessage({ message, onDismiss }) {
  return (
    <div className="bg-red-500/20 border border-red-500 rounded-lg p-4 mb-6 backdrop-blur-lg">
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <span className="text-2xl mr-3">⚠️</span>
          <div>
            <p className="font-semibold">Erreur</p>
            <p className="text-sm text-red-100">{message}</p>
          </div>
        </div>
        {onDismiss && (
          <button
            onClick={onDismiss}
            className="text-white hover:text-red-200 font-bold text-xl"
            aria-label="Fermer"
          >
            ×
          </button>
        )}
      </div>
    </div>
  );
}

export default ErrorMessage;
