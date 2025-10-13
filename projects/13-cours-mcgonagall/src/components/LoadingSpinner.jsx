function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-white mb-4"></div>
      <p className="text-lg text-purple-200">
        🔮 Récupération de l'emploi du temps magique...
      </p>
    </div>
  );
}

export default LoadingSpinner;
